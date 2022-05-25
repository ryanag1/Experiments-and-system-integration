using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Floor : MonoBehaviour
{
    public GameObject Atom;
    public int Width;
    public int Height;
    public int[,] Coordinate;
    // Start is called before the first frame update
    void Start()
    {
        for (int i = 0; i < Width; i++) {
            for (int j = 0; j < Height; j++) {
                Instantiate(Atom,transform.position+(new Vector3(i,0,j)),transform.rotation);
            }
        }
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void Init() {
        Width = 10;
        Height = 10;
        Coordinate = new int[Width, Height];
    }
}
