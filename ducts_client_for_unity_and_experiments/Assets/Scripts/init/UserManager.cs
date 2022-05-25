using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class UserManager : MonoBehaviour
{
    static public int UserId;
    public int player_num;
    static public int UserNum;
    public float[] init_position = new float[2];
    static public GameObject InstancePC; 
    static public GameObject[] InstanceNPC;
    static public GameObject MainCamera;
    static public int[] LoginId;
    // Start is called before the first frame update
    void Start()
    {
        UserManager.UserNum = this.player_num;
        DuctsRoot.ducts.OnOpenSetEventHandler("UserIdManage", (rid, eid, data) => {
            Debug.Log("<UserIdManage> rid: " + rid + ", eid: " + eid + ", UserId: " + data.num );
            UserManager.UserId = data.num;
            //UserManager.LoginId = data.intArray;
            //Debug.Log(UserManager.LoginId);
            //for (int i = 0; i < UserManager.LoginId.Length; i++)
            //{
                //Debug.Log(UserManager.LoginId[i]);
            //}
 

            Data d = new Data(); d.num = UserManager.UserId; 
            DuctsRoot.ducts.AckAllPlayersTransform(d);
            
            d.user_num = UserManager.UserNum; d.floatArray = init_position;
           //Debug.Log(UserManager.UserNum);
            //Debug.Log(UserManager.UserId);
            DuctsRoot.ducts.UserInit(d);

            //Data d2 = new Data(); d2.floatArray = new float[]{transform.position.x, transform.position.z}; d2.str = "<INIT>"; d2.num = UserManager.UserId; d2.user_num = UserManager.UserNum;
            //DuctsRoot.ducts.AckCoordinate(d2);
            //Debug.Log(data.intArray[0]);
            //Debug.Log(data.intArray[1]);
            //Debug.Log(data.intArray[2]);
        });
        DuctsRoot.ducts.OnOpenSetEventHandler("AliveMonitoring", (rid, eid, data) => {
            Debug.Log("ALIVE_MONITORING!");
        });
        UserManager.MainCamera = GameObject.FindWithTag("MainCamera");
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
