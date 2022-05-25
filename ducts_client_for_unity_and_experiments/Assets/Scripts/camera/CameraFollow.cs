using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraFollow : MonoBehaviour
{
    Vector3 diff;

    //public GameObject target;
    Transform targetTransform;
    public float followSpeed;

    public Vector3 cameraPosition;
    public float cameraAngle;
    bool init;

    // Start is called before the first frame update
    void Start()
    {
        this.init = false;
        /*Debug.Log(trarget.transform.position);
        transform.position = trarget.transform.position + cameraPosition;
        //transform.position = trarget.transform.position + new Vector3(0, 5, 0);
        transform.rotation = Quaternion.Euler(cameraAngle, 0, 0);
        diff = trarget.transform.position - transform.position;*/
    }

    // Update is called once per frame
    void Update()
    {
        if(this.init) {
            transform.position = Vector3.Lerp(
                transform.position,
                this.targetTransform.position - diff,
                Time.deltaTime * followSpeed
            );
        }
    }

    public void Init(Transform TargetTransform) {
        this.targetTransform = TargetTransform;
        transform.position = this.targetTransform.position + cameraPosition;
        //transform.position = trarget.transform.position + new Vector3(0, 5, 0);
        transform.rotation = Quaternion.Euler(cameraAngle, 0, 0);
        diff = this.targetTransform.position - transform.position;
        this.init = true;
        
    }
}
