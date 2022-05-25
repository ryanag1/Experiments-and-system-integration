namespace Name
{
    


using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using WebSocketSharp;
using System;
//using UnityEngine.Events;

[System.Serializable]
public class Response
{
    public string websocket_host;
    public string websocket_url;
    public string websocket_url_reconnect;
    public string api_host;
    public string api_url_root;
    public string api_url_event;

    public Event EVENT;
}

[System.Serializable]
public class Event
{
    public int ALIVE_MONITORING;
    public int LOGGING;
    public int PING;
    public int REDIS_EXECUTE;
    public int CLOSE_SESSION;
    public int CREATE_SESSION;
    public int LOGIN_FIRST_PAGE;
    public int FETCH_ALL_ACTIVE;
    public int ADD_DATA_FOR_SPECIFIC_USER;
    public int FETCH_DATA_FROM_SPECIFIC_USER;
    public int MEDIA_TRANSFORM;
    public int PING_PONG;
    public int CSV_WRITER;
    public int GET_REDIS_TABLE;
    public int RUN_SCRAPE;
    public int TEST_JSON_SERVER;
}

public static class TimeUtil {

    private static DateTime UnixEpoch = new DateTime(1970, 1, 1, 0, 0, 0, 0);

    // DateTimeからUnixTimeへ変換
    public static long GetUnixTime(DateTime dateTime)
    {
        return (long)(dateTime - UnixEpoch).TotalSeconds;
    }

    // UnixTimeからDateTimeへ変換
    public static DateTime GetDateTime(long unixTime)
    {
        return UnixEpoch.AddSeconds(unixTime);
    }
}

[System.Serializable]
public class DuctEvent
{
    public int request_id;
    public int event_id;
    public Data data;
}

[System.Serializable]
public class Data
{
    public int num;
    public string ver;
}

public class FetchJson : MonoBehaviour
{
    WebSocket ws;
    int _last_id;
    Event EVENT;
    Dictionary<int, Action<int,int, Data>> _event_handler;
    

    // Start is called before the first frame update
    void Start()
    {
        this.init();
        //StartCoroutineを使って実行
        StartCoroutine(this.Method());
        //Debug.Log(this.next_rid());
    }

    void init() {
        this._event_handler = new Dictionary<int, Action<int, int, Data>>();
    }

    int next_rid(){
        int next_id = (int) TimeUtil.GetUnixTime(DateTime.Now);
        if (next_id <= this._last_id) {
            next_id = this._last_id + 1;
        }
        this._last_id = next_id;
        return next_id;
    }

    private IEnumerator Method(){

        //1.UnityWebRequestを生成
        UnityWebRequest request = UnityWebRequest.Get("https://dev.riang.work/ducts/wsd?uuid=11");
        //UnityWebRequest request = UnityWebRequest.Get("http://localhost:8080/ducts/wsd?uuid=11");
        request.SetRequestHeader("User-Agent", "");

        //2.SendWebRequestを実行し、送受信開始
        yield return request.SendWebRequest();

        //3.isNetworkErrorとisHttpErrorでエラー判定
        if(request.isHttpError || request.isNetworkError) {
            //4.エラー確認
            Debug.Log(request.error);
        }
        else{
            //4.結果確認
            Debug.Log(request.downloadHandler.text);
            Response res = JsonUtility.FromJson<Response>(request.downloadHandler.text);
    
            //インスタンスの内容確認
            Debug.Log(res.websocket_url);
            Debug.Log(res.websocket_url.GetType());
            Debug.Log(res.EVENT.TEST_JSON_SERVER);
            this.EVENT = res.EVENT;

            ws = new WebSocket(res.websocket_url);

            ws.OnOpen += (sender, e) =>
            {
                Debug.Log("WebSocket Open");
                this.SetEventHandler(this.EVENT.TEST_JSON_SERVER, (rid, eid, data) => {
                    Debug.Log("InvokeEventHandler rid: " + rid + ", eid: " + eid + ", data.num: " + data.num + ", data.ver: " + data.ver);
                });
            };
            ws.OnMessage += (sender, e) =>
            {
                //Debug.Log("WebSocket Message Type: " + e.IsText + ", " +e.IsBinary + ", Data: " + e.Data);
                this._onmessage(e.Data);

            };
            ws.OnError += (sender, e) =>
            {
                Debug.Log("WebSocket Error Message: " + e.Message);
            };

            ws.OnClose += (sender, e) =>
            {
                Debug.Log("WebSocket Close");
            };
            try {
                //SSH接続するならコメントアウト外す
                ws.SslConfiguration.EnabledSslProtocols = System.Security.Authentication.SslProtocols.Tls12;
                ws.Connect();
            } catch(System.Exception e) {
                Debug.Log(e);
            }
        }

    }

    void _onmessage(string jsonDuctEvent) {
        DuctEvent ductEvent = JsonUtility.FromJson<DuctEvent>(jsonDuctEvent);
        int rid = ductEvent.request_id;
        int eid = ductEvent.event_id;
        Data data = ductEvent.data;
        Action<int,int,Data> handler = this._event_handler[eid];
        handler(rid, eid, data);
        //Debug.Log(rid);
        //Debug.Log(eid);
        //Debug.Log(data.num);
        //Debug.Log(data.ver);
        
    }

    void SetEventHandler(int event_id, Action<int, int, Data> handler) {
        this._event_handler.Add(event_id, handler);
    }



    void Update()
    {

        if (Input.GetKeyUp("s"))
        {
            DuctEvent ductEvent = new DuctEvent();
            ductEvent.request_id = this.next_rid();
            ductEvent.event_id = this.EVENT.TEST_JSON_SERVER;
            Data data = new Data();
            data.num = 234;
            data.ver = "Hello,World";
            ductEvent.data = data;
            string json = JsonUtility.ToJson(ductEvent);
            ws.Send(json);
        }

    }

    void OnDestroy()
    {
        ws.Close();
        ws = null;
    }
}


}