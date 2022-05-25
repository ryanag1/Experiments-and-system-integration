using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DuctsRoot : MonoBehaviour
{
    static public Ducts ducts;

    void init() {
        DuctsRoot.ducts = new Ducts();
    }
    // Start is called before the first frame update
    void Start()
    {
        init();
        StartCoroutine(DuctsRoot.ducts.Open());
        //Debug.Log(ducts.EVENT);
        //DuctsRoot.ducts.OnOpenSetEventHandler("TestJsonServer", (rid, eid, data) => {
            //Debug.Log("<InvokeEventHandler> rid: " + rid + ", eid: " + eid + ", data.num: " + data.num + ", data.ver: " + data.ver);
        //});
        
    }

    // Update is called once per frame
    void Update()
    {
        /*if (Input.GetKeyUp("s"))
        {
            Data data = new Data();
            data.num = 123;
            data.str = "DuctsRoot";
            DuctsRoot.ducts.TestJsonServer(data);
        }*/
    }

    void OnDestroy() {
        DuctsRoot.ducts.Close();
    }
}
