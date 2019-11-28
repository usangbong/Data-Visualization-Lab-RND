using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Test2 : MonoBehaviour
{
    bool startColor;

    void Start()
    {
        startColor = false;
    }

    void Update()
    {
        if(Input.GetKeyDown(KeyCode.Q))
        {
            startColor = true;
        }

        if(startColor)
        {
            gameObject.transform.GetComponent<MeshRenderer>().material.color -= new Color(0, 0, 0, 0.01f);
        }
    }
}
