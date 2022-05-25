using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CharaController : MonoBehaviour
{
    const float MAXRIGHT = 5.0f;
    const float MINLEFT = -5.0f;
    const float MAXFRONT = -2.5f;
    
    const float jumpHighThreshold = 0.2f;
    const float thresholdJumpHighest = 0.2f;
    CharacterController controller;
    Animator animator;

    Vector3 moveDirection = Vector3.zero;

    public float gravity;
    public float recoverySpeed;
    public float speedX;
    public float speedXZ;
    public float speedJump;
    public float speedJumpHigh;
    public float speedJumpHighest;
    float jumpHighTime = 0.0f;
    float timeJumpHighest = 0.0f;
    public int id;
    //bool w = false, s = false, a = false, d = false;
    //public int id;
    // Start is called before the first frame update
    void Start()
    {
        controller = GetComponent<CharacterController>();
        //animator = GetComponent<Animator>();
        /*DuctsRoot.ducts.OnOpenSetEventHandler("TestJsonServer", (rid, eid, data) => {
            Debug.Log("<InvokeEventHandler> rid: " + rid + ", eid: " + eid + ", data.num: " + data.num + ", data.ver: " + data.str);
            Debug.Log(data.intArray[0]);
            Debug.Log(data.intArray[1]);
            Debug.Log(data.intArray[2]);
        });
        DuctsRoot.ducts.OnOpenSetEventHandler("AckAllPlayersTransform", (rid, eid, data) => {
            //Debug.Log("<AckAllPlayersTransform> rid: " + rid + ", eid: " + eid + ", data.num: " + data.num + ", data.ver: " + data.str);
            if(id == data.num) {
                Debug.Log(data.floatArray[0]);
                Debug.Log(data.floatArray[1]);
                if(data.str == "dd") this.d = true;
                else if(data.str == "du") this.d = false;
                else if (data.str == "ad") this.a = true;
                else if (data.str == "au") this.a = false;  

                if(data.str == "wd") this.w = true;
                else if(data.str == "wu") this.w = false;
                else if (data.str == "sd") this.s = true;
                else if (data.str == "su") this.s = false;  
            }
        });*/
        //Data d = new Data(); d.intArray = new int[] {1234, 345}; d.num = 1; d.str = "HE++";
        //DuctsRoot.ducts.AckAllPlayersTransform(d);
    }

    // Update is called once per frame
    void Update()
    {
        if (controller.isGrounded)
        {
            
            
            if ( AllPlayersTransform.AllPlayersCommands[this.id][0]  && Condition(false, "MAXRIGHT") ) 
            {
                //moveDirection.z = Input.GetAxis("Horizontal") * speedXZ;
                moveDirection.x = 1 * speedX;
            }
            else if ( AllPlayersTransform.AllPlayersCommands[this.id][1] && Condition(false, "MINRIGHT") )
            {
                //moveDirection.z = -1 * Input.GetAxis("Horizontal") * speedXZ;
                moveDirection.x = -1 * speedX;
            }
            else
            //if (  !AllPlayersTransform.AllPlayersCommands[this.id][0] && ! AllPlayersTransform.AllPlayersCommands[this.id][1] )
            {
                moveDirection.x = 0;
                
            }

            if ( AllPlayersTransform.AllPlayersCommands[this.id][2] && Condition(false, "MAXHEIGHT") ) 
            {
                //moveDirection.z = Input.GetAxis("Horizontal") * speedXZ;
                //Debug.Log("w");
                moveDirection.z = 1 * speedX;

                //if (Input.GetKeyDown("w")) {
                    //Data data = new Data(); data.num = 321; data.str = "Key: w"; data.intArray = new int[] { 6, 5, 4 };
                    //DuctsRoot.ducts.TestJsonServer(data);
                //}
            }
            else if ( AllPlayersTransform.AllPlayersCommands[this.id][3] && Condition(false, "MINBOTTOM") )
            {
                //moveDirection.z = -1 * Input.GetAxis("Horizontal") * speedXZ;
                moveDirection.z = -1 * speedX;
                //if (Input.GetKeyDown("s"))
                //{
                   // Data data = new Data(); data.num = 123; data.str = "Key: s"; data.intArray = new int[] { 4, 5, 6 };
                    //DuctsRoot.ducts.TestJsonServer(data);
               // }
            }
            //if (  !AllPlayersTransform.AllPlayersCommands[this.id][2] && ! AllPlayersTransform.AllPlayersCommands[this.id][3] )
            else
            {
                
                moveDirection.z = 0;
            }


            if (AllPlayersTransform.AllPlayersCommands[this.id][4])
            {
                if(jumpHighTime <= 0.0f && timeJumpHighest <= 0.0f) 
                {
                    moveDirection.y = speedJump;
                    //animator.SetTrigger("jump");
                    jumpHighTime = jumpHighThreshold;
                }
                else if (timeJumpHighest <= 0.0f)
                {
                    moveDirection.y = speedJumpHigh;
                    //animator.SetTrigger("jumpHigh");
                    jumpHighTime = 0.0f;
                    timeJumpHighest = thresholdJumpHighest;
                }
                else
                {
                    moveDirection.y = speedJumpHighest;
                    //animator.SetTrigger("jumpHighest");
                    timeJumpHighest = 0.0f;
                }
            }

            if ( jumpHighTime > 0.0f ) 
            {
                jumpHighTime -= Time.deltaTime;
            }

            if ( timeJumpHighest > 0.0f ) 
            {
                timeJumpHighest -= Time.deltaTime;
            }

            if( Condition(false, "MAXFRONT") )
            {
                //moveDirection.z = recoverySpeed * Time.deltaTime;
            }
            
        }


        //if ( !CharaCorrectTransform.correct ) {
        transform.position = new Vector3(AllPlayersTransform.AllPlayersPosition[this.id][0], 1, AllPlayersTransform.AllPlayersPosition[this.id][1]);
            
        moveDirection.y -= gravity * Time.deltaTime;

        Vector3 globalDirection = transform.TransformDirection(moveDirection);
        controller.Move(globalDirection * Time.deltaTime);

        if(controller.isGrounded) moveDirection.y = 0;
        //}
        //else {
            //CharaCorrectTransform.correct = false;
        //}
        //animator.SetBool("left", moveDirection.x < 0.0f); 
        //animator.SetBool("right", moveDirection.x > 0.0f); 
        
    }
    
    bool Condition(bool on, string cond){
        if(!on) return true;
        else if (cond == "MAXRIGHT") 
        {
            return transform.position.x < MAXRIGHT;
        } 
        else if( cond == "MINLEFT" )
        {
            return transform.position.x < MINLEFT;
        }
        else if( cond == "MAXFRONT" )
        {
            return transform.position.z < MAXFRONT;
        }
        return false;
    }

    void CorrectCoordinate() {
        transform.position = new Vector3(AllPlayersTransform.AllPlayersPosition[this.id][0], 1, AllPlayersTransform.AllPlayersPosition[this.id][1]);
    }

}
