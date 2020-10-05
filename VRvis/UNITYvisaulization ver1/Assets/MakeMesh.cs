using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using IATK;
public class MakeMesh : MonoBehaviour
{
    public BigMesh bigMesh;
    bool isSave = false;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if (!isSave)
        {
            bigMesh.SaveBigMesh();
            isSave = true;
        }
    }
}
