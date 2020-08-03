using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LargeSmallCollider : MonoBehaviour
{
    public Vector3 max, min;
    public float perX, perY, perZ;
    public float speed;
    bool left, right;

    Final final;

    private void Start()
    {
        final = GameObject.Find("GameManager").GetComponent<Final>();
        left = right = false;
    }

    private void Update()
    {
        if (!final.timeFin)
        {
            if (left && gameObject.transform.localScale.x >= min.x &&
                gameObject.transform.localScale.y >= min.y &&
                gameObject.transform.localScale.z >= min.z)
            {
                gameObject.transform.localScale -= new Vector3(speed * perX, speed * perY, speed * perZ);
            }

            if (right && gameObject.transform.localScale.x <= max.x &&
                gameObject.transform.localScale.y <= max.y &&
                gameObject.transform.localScale.z <= max.z)
            {
                gameObject.transform.localScale += new Vector3(speed * perX, speed * perY, speed * perZ);
            }
        }
    }

    private void OnTriggerEnter(Collider other)
    {
        if(other.name == "Traker (left)")
        {
            left = true;
        }

        if(other.name == "Traker (right)")
        {
            right = true;
        }
    }

    private void OnTriggerExit(Collider other)
    {
        if(other.name == "Traker (left)")
        {
            left = false;
        }

        if(other.name == "Traker (right)")
        {
            right = false;
        }
    }
}
