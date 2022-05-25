using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NpcSpawn : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        DuctsRoot.ducts.OnOpenSetEventHandler("UserInit", (rid, eid, data) => {
            Debug.Log("UserInit");        
            Debug.Log(data.num);
            Debug.Log(data.user_num);
            Debug.Log(data.floatArray[0]);
            Debug.Log(data.floatArray[1]);
        });
        
    }

    // Update is called once per frame
    void Update()
    {
        if(Input.GetKey("q")) {
            Data data2 = new Data(); data2.str = "NpcSpawn";
            //DuctsRoot.ducts.UserInit(data2);
        }
    }
}
