using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CharaCorrectTransform : MonoBehaviour
{
    CharacterController controller;
    public int id; 
    public static bool correct;
    // Start is called before the first frame update
    void Start()
    {
        controller = GetComponent<CharacterController>();
    }

    // Update is called once per frame
    void Update()
    {
        if(controller.isGrounded) {
            if (AllPlayersTransform.AllPlayersPositionQueue.Count != 0) {
                float[][] allPlayersPosition = AllPlayersTransform.AllPlayersPositionQueue.Dequeue();
                Vector3 Correct = new Vector3(allPlayersPosition[this.id][0], 1, allPlayersPosition[this.id][1]);
                if( (transform.position - Correct).x > 1.0 || (transform.position - Correct).x < -1.0 || (transform.position - Correct).z > 1.0 || (transform.position - Correct).z < -1.0 )
                {
                    correct = true;
                    transform.position = Correct;
                    Debug.Log("Correct: " + this.id);
                    Debug.Log(Correct);
                }
            }
        }
    }
}
