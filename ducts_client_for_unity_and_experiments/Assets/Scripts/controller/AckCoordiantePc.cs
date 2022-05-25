using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AckCoordiantePc : MonoBehaviour
{
    // Start is called before the first frame update
    public int id;
    void Start()
    {
        DuctsRoot.ducts.OnOpenSetEventHandler("AckCoordinate", (rid, eid, data) => {
            Debug.Log("<InvokeEventHandler> rid: " + rid + ", eid: " + eid + ", data.num: " + data.num + ", data.ver: " + data.str);
            //Debug.Log(data.floatArray[0]);
            //Debug.Log(data.floatArray[1]);
        });
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKeyDown("a")) {
            Data data = new Data(); data.floatArray = new float[]{transform.position.x, transform.position.z}; data.str = "ad"; data.num = UserManager.UserId; data.user_num = UserManager.UserNum; data.intArray = UserManager.LoginId;
            DuctsRoot.ducts.AckCoordinate(data);
        } 
        else if(Input.GetKeyUp("a")) {
            Data data = new Data(); data.floatArray = new float[]{transform.position.x, transform.position.z}; data.str = "au"; data.num = UserManager.UserId; data.user_num = UserManager.UserNum; data.intArray = UserManager.LoginId;
            DuctsRoot.ducts.AckCoordinate(data);
        }
        if(Input.GetKeyDown("d")) {
            Data data = new Data(); data.floatArray = new float[]{transform.position.x, transform.position.z}; data.str = "dd"; data.num = UserManager.UserId; data.user_num = UserManager.UserNum; data.intArray = UserManager.LoginId;
            DuctsRoot.ducts.AckCoordinate(data);
        }
        else if(Input.GetKeyUp("d")) {
            Data data = new Data(); data.floatArray = new float[]{transform.position.x, transform.position.z}; data.str = "du"; data.num = UserManager.UserId; data.user_num = UserManager.UserNum; data.intArray = UserManager.LoginId;
            DuctsRoot.ducts.AckCoordinate(data);
        }


        if (Input.GetKeyDown("w")) {
            Data data = new Data(); data.floatArray = new float[]{transform.position.x, transform.position.z}; data.str = "wd"; data.num = UserManager.UserId; data.user_num = UserManager.UserNum; data.intArray = UserManager.LoginId;
            DuctsRoot.ducts.AckCoordinate(data);
        } 
        else if(Input.GetKeyUp("w")) {
            Data data = new Data(); data.floatArray = new float[]{transform.position.x, transform.position.z}; data.str = "wu"; data.num = UserManager.UserId; data.user_num = UserManager.UserNum; data.intArray = UserManager.LoginId;
            DuctsRoot.ducts.AckCoordinate(data);
        }
        if(Input.GetKeyDown("s")) {
            Data data = new Data(); data.floatArray = new float[]{transform.position.x, transform.position.z}; data.str = "sd"; data.num = UserManager.UserId; data.user_num = UserManager.UserNum; data.intArray = UserManager.LoginId;
            DuctsRoot.ducts.AckCoordinate(data);
        }
        else if(Input.GetKeyUp("s")) {
            Data data = new Data(); data.floatArray = new float[]{transform.position.x, transform.position.z}; data.str = "su"; data.num = UserManager.UserId; data.user_num = UserManager.UserNum; data.intArray = UserManager.LoginId;
            DuctsRoot.ducts.AckCoordinate(data);
        }

        if(Input.GetKeyDown("space")) {
            Data data = new Data(); data.floatArray = new float[]{transform.position.x, transform.position.z}; data.str = "spaced"; data.num = UserManager.UserId; data.user_num = UserManager.UserNum; data.intArray = UserManager.LoginId;
            DuctsRoot.ducts.AckCoordinate(data);
        }
        else if(Input.GetKeyUp("space")) {
            Data data = new Data(); data.floatArray = new float[]{transform.position.x, transform.position.z}; data.str = "spaceu"; data.num = UserManager.UserId; data.user_num = UserManager.UserNum; data.intArray = UserManager.LoginId;
            DuctsRoot.ducts.AckCoordinate(data);
        }
    }
}
