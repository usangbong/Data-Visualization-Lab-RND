using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Colliders : MonoBehaviour
{
    int num;
    CameraMove cameraMove;
    bool start;

    void Start()
    {
        start = false;
        cameraMove = GameObject.Find("CameraMoveManager").GetComponent<CameraMove>();

        if(gameObject.name == "Front")
        {
            num = 0;
        }

        else if(gameObject.name == "Back")
        {
            num = 1;
        }

        else if(gameObject.name == "Left")
        {
            num = 2;
        }

        else if(gameObject.name == "Right")
        {
            num = 3;
        }

        else if(gameObject.name == "Up")
        {
            num = 4;
        }

        else if(gameObject.name == "Down")
        {
            num = 5;
        }

        Invoke("Starts", 1.0f);
    }

    void Starts()
    {
        start = true;
    }

    private void OnTriggerEnter(Collider other)
    {
        if (start)
        {
            if (other.name == "Traker (left)")
            {
                cameraMove.leftList[num] = true;
            }

            if (other.name == "Traker (right)")
            {
                cameraMove.rightList[num] = true;
            }
        }
    }

    private void OnTriggerExit(Collider other)
    {
        if (start)
        {
            if (other.name == "Traker (left)")
            {
                cameraMove.leftList[num] = false;
            }

            if (other.name == "Traker (right)")
            {
                cameraMove.rightList[num] = false;
            }
        }
    }
}
