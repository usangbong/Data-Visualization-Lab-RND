using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LargeSmallColliderGm : MonoBehaviour
{
    public GameObject gm;
    public Vector3 max, min;
    public float perX, perY, perZ;
    public float speed;
    bool left, right;

    Final final;

    private void Start()
    {
        left = right = false;
        final = GameObject.Find("GameManager").GetComponent<Final>();
    }

    private void Update()
    {
        if (!final.timeFin)
        {
            if (left && gm.transform.localScale.x >= min.x &&
                gm.transform.localScale.y >= min.y &&
                gm.transform.localScale.z >= min.z)
            {
                gm.transform.localScale -= new Vector3(speed * perX, speed * perY, speed * perZ);
            }

            if (right && gm.transform.localScale.x <= max.x &&
                gm.transform.localScale.y <= max.y &&
                gm.transform.localScale.z <= max.z)
            {
                gm.transform.localScale += new Vector3(speed * perX, speed * perY, speed * perZ);
            }
        }
    }

    private void OnTriggerEnter(Collider other)
    {
        if (other.name == "Traker (left)")
        {
            left = true;
        }

        if (other.name == "Traker (right)")
        {
            right = true;
        }
    }

    private void OnTriggerExit(Collider other)
    {
        if (other.name == "Traker (left)")
        {
            left = false;
        }

        if (other.name == "Traker (right)")
        {
            right = false;
        }
    }
}
