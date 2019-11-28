using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EyeColliding : MonoBehaviour
{
    Eye eye;

    void Start()
    {
        eye = GameObject.Find("EyeManager").GetComponent<Eye>();
    }

    void OnTriggerEnter(Collider other)
    {
        if (other.tag == "Tracker")
        {
            eye.time10 = true;
        }
    }
}
