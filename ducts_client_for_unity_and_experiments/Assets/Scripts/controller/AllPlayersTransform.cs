using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AllPlayersTransform : MonoBehaviour
{
    // Start is called before the first frame update
    public struct NPCTransform
    {
        //public bool w = false, s = false, a = false, d = false;
        public bool w;
        public bool s;
        public bool a;
        public bool d;

    };
    static public bool w = false, s = false, a = false, d = false;
    //public int id;
    //static public NPCTransform[] nPCTransforms;
    static public bool[][] AllPlayersCommands; 
    static public float[][] AllPlayersPosition;
    static public Queue<float[][]> AllPlayersPositionQueue;
    public int players_num = UserManager.UserNum;

    // Start is called before the first frame update
    void Start()
    {
        AllPlayersPosition = new float[UserManager.UserNum][];
        AllPlayersCommands = new bool[UserManager.UserNum][];
        AllPlayersPositionQueue = new Queue<float[][]>();
        for (int i = 0; i < UserManager.UserNum; i++ ) {
            AllPlayersCommands[i] = new bool[] {false, false, false, false, false};
            AllPlayersPosition[i] = new float[] {0,0};
        }
        DuctsRoot.ducts.OnOpenSetEventHandler("TestJsonServer", (rid, eid, data) => {
            Debug.Log("<InvokeEventHandler> rid: " + rid + ", eid: " + eid + ", data.num: " + data.num + ", data.ver: " + data.str);
            Debug.Log(data.intArray[0]);
            Debug.Log(data.intArray[1]);
            Debug.Log(data.intArray[2]);
        });
        DuctsRoot.ducts.OnOpenSetEventHandler("AckAllPlayersTransform", (rid, eid, data) => {
            Debug.Log("<AckAllPlayersTransform> rid: " + rid + ", eid: " + eid + ", data.num: " + data.num + ", data.ver: " + data.str + ", data.intArray: " + data.intArray[0]);
            
            
            if(data.str == "dd") AllPlayersCommands[data.num][0] = true;
            if(data.str == "du") AllPlayersCommands[data.num][0] = false; //AllPlayersPosition[data.num][0] = data.floatArray[0]; AllPlayersPosition[data.num][1] = data.floatArray[1]; AllPlayersPositionQueue.Enqueue(AllPlayersPosition);
            if (data.str == "ad") AllPlayersCommands[data.num][1] = true;
            if (data.str == "au") AllPlayersCommands[data.num][1] = false; //AllPlayersPosition[data.num][0] = data.floatArray[0]; AllPlayersPosition[data.num][1] = data.floatArray[1]; AllPlayersPositionQueue.Enqueue(AllPlayersPosition); 

            if(data.str == "wd") AllPlayersCommands[data.num][2] = true;
            if(data.str == "wu") AllPlayersCommands[data.num][2] = false; //AllPlayersPosition[data.num][0] = data.floatArray[0]; AllPlayersPosition[data.num][1] = data.floatArray[1]; AllPlayersPositionQueue.Enqueue(AllPlayersPosition);
            if (data.str == "sd") AllPlayersCommands[data.num][3] = true;
            if (data.str == "su") AllPlayersCommands[data.num][3] = false; //AllPlayersPosition[data.num][0] = data.floatArray[0]; AllPlayersPosition[data.num][1] = data.floatArray[1]; AllPlayersPositionQueue.Enqueue(AllPlayersPosition);  

            if (data.str == "spaced") AllPlayersCommands[data.num][4] = true;
            if (data.str == "spaceu") AllPlayersCommands[data.num][4] = false;

            AllPlayersPosition[data.num][0] = data.floatArray[0];
            AllPlayersPosition[data.num][1] = data.floatArray[1];
            //AllPlayersPositionQueue.Enqueue(AllPlayersPosition);
        });
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
