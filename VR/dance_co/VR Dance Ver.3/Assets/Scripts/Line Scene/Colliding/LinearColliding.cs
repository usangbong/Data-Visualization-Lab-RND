using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LinearColliding : MonoBehaviour
{
    CircleMove circleMove;
    Linear linear;

    void Start()
    {
        circleMove = GameObject.Find("WaveManager").GetComponent<CircleMove>();
        linear = GameObject.Find("LinearManager").GetComponent<Linear>();
    }

    private void OnTriggerEnter(Collider other)
    {
        if(other.tag == "Tracker")
        {
            if(circleMove.animFinish && !linear.ArrowMake)
            {
                linear.ArrowMake = true;
            }
        }
    }
}
