using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Cell: MonoBehaviour
{
    private bool state;

    private void Awake()
    {
        state = false;
        GetComponent<MeshRenderer>().material.color = Color.white;
    }

    public bool getState() { return state; }

    public void setObject() 
    { 
        state = true;
        GetComponent<MeshRenderer>().material.color = Color.black;
    }

    public void removeObject() 
    { 
        state = false;
        GetComponent<MeshRenderer>().material.color = Color.white;
    }
}
