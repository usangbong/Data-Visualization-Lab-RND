using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HeartColliding : MonoBehaviour
{
    Heart heart;

    void Start()
    {
        heart = GameObject.Find("HeartManager").GetComponent<Heart>();
    }

    void OnTriggerEnter(Collider other)
    {
        if(other.tag == "Tracker")
        {
            if (heart.isMove)
            {
                heart.moveStart = true;

                heart.pos = diff(gameObject.transform.position, other.gameObject.transform.position);
            }
        }
    }

    Vector3 diff(Vector3 pos1, Vector3 pos2)
    {
        Vector3 d;
        d.x = pos1.x - pos2.x;
        d.y = pos1.y - pos2.y;
        d.z = pos1.z - pos2.z;

        return d;
    }
}
