using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HalfCircleColliding : MonoBehaviour
{
    Circle circle;
    Ring ring;
    bool isColliding;

    void Start()
    {
        circle = GameObject.Find("CircleManager").GetComponent<Circle>();
        ring = GameObject.Find("RingManager").GetComponent<Ring>();
        isColliding = false;
    }

    void OnTriggerEnter(Collider other)
    {
        if(other.tag == "Tracker")
        {
            if (!circle.sizes && !circle.turns && !isColliding)
            {
                circle.turns = true;
                isColliding = true;
                circle.cnt++;
            }

            if(!circle.sizes && circle.turns && !isColliding)
            {
                circle.turns = false;
                isColliding = true;
                circle.cnt++;
            }

            if(circle.CircleFinish && !isColliding && circle.turns)
            {
                isColliding = true;
                circle.turns = false;
            }

            if(circle.CircleFinish && !isColliding && !circle.turns)
            {
                isColliding = true;
                circle.turns = true;
            }
        }
    }

    void OnTriggerExit(Collider other)
    {
        if(other.tag == "Tracker")
        {
            isColliding = false;
        }
    }
}
