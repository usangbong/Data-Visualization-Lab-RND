using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class RingParentColliding : MonoBehaviour
{
    Circle circle;

    void Start()
    {
        circle = GameObject.Find("CircleManager").GetComponent<Circle>();
    }

    private void OnTriggerEnter(Collider other)
    {
        if(other.tag == "Tracker")
        {
            if(circle.returnColor && circle.isBlinking)
            {
                circle.isBlinking = false;
            }
        }
    }
}
