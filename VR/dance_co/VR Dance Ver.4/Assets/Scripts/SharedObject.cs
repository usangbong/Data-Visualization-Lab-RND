using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SharedObject : MonoBehaviour
{
    public GameObject SelectObject, SelectBluePrint;

    void Start()
    {
        SelectObject = SelectBluePrint = null;
    }
}
