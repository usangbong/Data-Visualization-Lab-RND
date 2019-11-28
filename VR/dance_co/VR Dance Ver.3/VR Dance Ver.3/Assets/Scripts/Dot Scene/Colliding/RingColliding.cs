using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class RingColliding : MonoBehaviour
{
    Ring ring;
    bool isColliding;
    bool isCol2;

    void Start()
    {
        ring = GameObject.Find("RingManager").GetComponent<Ring>();
        isColliding = isCol2 = false;
    }

    private void OnTriggerEnter(Collider other)
    {
        if(other.tag == "Tracker")
        {
            if(!isColliding)
            {
                ChangeColor();
                ring.cnt++;
                isColliding = true;
            }

            if(isColliding)
            {
                ChangeColor();
            }
        }
    }

    private void OnTriggerExit(Collider other)
    {
        if(other.tag == "Tracker")
        {
            isCol2 = false;
        }
    }

    void ChangeColor()
    {
        gameObject.transform.GetComponent<MeshRenderer>().material.color = new Color(Random.value, Random.value, Random.value);
    }
}
