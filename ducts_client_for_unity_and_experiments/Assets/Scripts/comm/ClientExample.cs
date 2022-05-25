using UnityEngine;
using System.Collections;
using WebSocketSharp;
using WebSocketSharp.Net;


[System.Serializable]
public class MyClass
{
    public int level;
    public float timeElapsed;
    public string playerName;
}

public class ClientExample: MonoBehaviour {

    WebSocket ws;
    MyClass myObject;

    void Start()
    {
        Debug.Log("HELLO");
        ws = new WebSocket("ws://localhost:3000/");

        ws.OnOpen += (sender, e) =>
        {
            Debug.Log("WebSocket Open");
        };

        ws.OnMessage += (sender, e) =>
        {
            Debug.Log("WebSocket Message Type: " + e.IsText + ", " +e.IsBinary + ", Data: " + e.Data);
        };

        ws.OnError += (sender, e) =>
        {
            Debug.Log("WebSocket Error Message: " + e.Message);
        };

        ws.OnClose += (sender, e) =>
        {
            Debug.Log("WebSocket Close");
        };

        ws.Connect();

        myObject = new MyClass();
        myObject.level = 1;
        myObject.timeElapsed = 47.5f;
        myObject.playerName = "Dr Charles Francis";

    }

    void Update()
    {

        if (Input.GetKeyUp("s"))
        {
            string json = JsonUtility.ToJson(myObject);
            ws.Send(json);
        }

    }

    void OnDestroy()
    {
        if (ws != null) {
            ws.Close();
            ws = null;
        }
    }
}