using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TrackerColliding : MonoBehaviour
{
    ColorCircle cCircle;

    bool isColliding;

    void Start()
    {
        cCircle = GameObject.Find("ColorCircleManager").GetComponent<ColorCircle>();

        isColliding = false;
    }

    private void OnTriggerEnter(Collider other)
    {
        if(other.tag == "Tracker")
        {
            if (!cCircle.yellowStart && !isColliding && cCircle.torus && cCircle.torus2 && !cCircle.fin2)
            {
                cCircle.yellowStart = true;
                isColliding = true;
            }     

            if(!cCircle.changeStart && !isColliding && cCircle.ytorus && cCircle.ytorus2)
            {
                cCircle.changeStart = true;
                isColliding = true;
            }

            if (!cCircle.Ctorus && !isColliding && cCircle.changeStart)
            {
                cCircle.Ctorus = true;
                isColliding = true;
            }
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
