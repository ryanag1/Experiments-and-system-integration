using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class AllPlayersSpawn : MonoBehaviour
{
    public GameObject PC;
    public GameObject NPC;
    Queue<Data> queue = new Queue <Data>();
    // Start is called before the first frame update
    void Start()
    {
        UserManager.InstanceNPC = new GameObject[UserManager.UserNum];
        DuctsRoot.ducts.OnOpenSetEventHandler("UserInit", (rid, eid, data) => {
            Debug.Log("UserInit");        
            Debug.Log(data.num);
            Debug.Log(data.user_num);
            Debug.Log(data.floatArray[0]);
            Debug.Log(data.floatArray[1]);
            //Debug.Log("FLOAT2DARRAY");
            //Debug.Log(data.float2DArray[0,0]);
            //Debug.Log(data.float2DArray[0,0]);
            //Debug.Log(data.float2DArray[1,0]);
            //Debug.Log(data.float2DArray[1,1]);
            Debug.Log(data.intArray);
            Debug.Log(data.intArray[0]);
            UserManager.LoginId = data.intArray;
            
            queue.Enqueue(data);
        });
        
    }

    // Update is called once per frame
    void Update()
    {
        if(queue.Count > 0) {
            Data data = queue.Dequeue();
            Debug.Log(data.str);
            if ( data.str == "Login") {
                this.Spawn(data);
            }
            else if ( data.str == "Logout") {
                this.DestroyPlayer(data);
            }
        }
    }

    public void Spawn(Data data){
        try {
            Vector3 PlayerTransformPosition = new Vector3(data.floatArray[0], 1, data.floatArray[1]);
            Quaternion PlayerTransformRotate = new Quaternion(0, 0, 0, 0);

            if(data.num == UserManager.UserId) 
            {
                GameObject pc = (GameObject) Instantiate (this.PC, PlayerTransformPosition, PlayerTransformRotate);
                pc.transform.parent = this.transform;
                pc.GetComponent<CharaController>().id = UserManager.UserId;
                //pc.GetComponent<CharaCorrectTransform>().id = UserManager.UserId;
                UserManager.MainCamera.GetComponent<CameraFollow>().Init(pc.transform);
                UserManager.InstancePC = pc;
            }
            else 
            {
                GameObject npc = (GameObject) Instantiate (this.NPC, PlayerTransformPosition, PlayerTransformRotate);
                npc.transform.parent = this.transform;
                npc.GetComponent<CharaController>().id = data.num;
                //npc.GetComponent<CharaCorrectTransform>().id = data.num;
                UserManager.InstanceNPC[data.num] = npc;
            }
        }
        catch(System.Exception e) {
            Debug.Log(e);
        }
    }

    public void DestroyPlayer(Data data) {
        Destroy(UserManager.InstanceNPC[data.num]);
    }
}
