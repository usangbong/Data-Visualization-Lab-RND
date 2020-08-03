using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class halfCollider : MonoBehaviour
{
    bool isColliding;

    void Start()
    {
        isColliding = false;
    }

    void Update()
    {
        if(isColliding)
        {
            gameObject.transform.rotation = Quaternion.Euler(0, 180, 0);
        }

        else
        {
            gameObject.transform.rotation = Quaternion.Euler(0, 0, 0);
        }
    }

    private void OnTriggerEnter(Collider other)
    {
        if(other.tag == "Tracker")
        {
            isColliding = true;
        }
    }

    private void OnTriggerExit(Collider other)
    {
        if(other.tag == "Tracker")
        {
            isColliding = false;
        }
    }
}
