using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BlueCircleColliding : MonoBehaviour
{
    CircleMove circleMove;

    bool isColliding;

    void Start()
    {
        circleMove = GameObject.Find("WaveManager").GetComponent<CircleMove>();
        isColliding = false;
    }

    private void OnTriggerEnter(Collider other)
    {
        if(other.tag == "Tracker")
        {
            if(!circleMove.blueColliding && !isColliding && circleMove.isMoveFinish)
            {
                circleMove.blueColliding = true;
                circleMove.isMoveFinish = false;
                isColliding = true;
            }
        }
    }

    private void OnTriggerExit(Collider other)
    {
        if (other.tag == "Tracker")
        {
            isColliding = false;
        }
    }
}
