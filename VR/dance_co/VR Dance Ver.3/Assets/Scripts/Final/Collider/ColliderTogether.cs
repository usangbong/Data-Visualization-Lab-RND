using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ColliderTogether : MonoBehaviour
{
    public GameObject nullPar, gm;
    public Vector3 max, min;
    public bool isColliding, posBool;
    ColliderTogether CT;

    private void Start()
    {
        isColliding = false;
        posBool = false;
    }

    private void Update()
    {
        if(!isColliding)
        {
            if(gm.transform.localScale.x <= max.x)
            {
                gm.transform.localScale += new Vector3(0.005f, 0, 0);
            }

            if(gm.transform.localScale.y <= max.y)
            {
                gm.transform.localScale += new Vector3(0, 0.005f, 0);
            }

            if(gm.transform.localScale.z <= max.z)
            {
                gm.transform.localScale += new Vector3(0, 0, 0.005f);
            }
        }

        else
        {
            if (gm.transform.localScale.x >= min.x)
            {
                gm.transform.localScale -= new Vector3(0.005f, 0, 0);
            }

            if (gm.transform.localScale.y >= min.y)
            {
                gm.transform.localScale -= new Vector3(0, 0.005f, 0);
            }

            if (gm.transform.localScale.z >= min.z)
            {
                gm.transform.localScale -= new Vector3(0, 0, 0.005f);
            }
        }

        if(posBool)
        {
            gm.transform.localPosition = new Vector3(0, 0, 0);
        }

    }

    private void OnTriggerEnter(Collider other)
    {
        if (other.tag == "Tracker" && !isColliding)
        {
            if (other.transform.childCount > 0)
            {
                if (other.transform.GetChild(0).tag == "flat")
                {
                    CT = other.transform.GetChild(0).GetChild(2).GetComponent<ColliderTogether>();
                    CT.posBool = false;
                    CT.isColliding = false;
                    CT.InvokeFunc();
                }

                else if(other.transform.GetChild(0).tag == "flat2")
                {
                    CT = other.transform.GetChild(0).GetChild(3).GetComponent<ColliderTogether>();
                    CT.posBool = false;
                    CT.isColliding = false;
                    CT.InvokeFunc();
                }

                else if (other.transform.GetChild(0).tag == "flat3")
                {
                    CT = other.transform.GetChild(0).GetChild(4).GetComponent<ColliderTogether>();
                    CT.posBool = false;
                    CT.isColliding = false;
                    CT.InvokeFunc();
                }
            }

            other.transform.DetachChildren();
            gm.transform.SetParent(other.transform);
            posBool = true;
            isColliding = true;
        }

        if (other.tag == "Column" && isColliding)
        {
            posBool = false;
            isColliding = false;
            gm.transform.SetParent(nullPar.transform);
        }
    }

    public void InvokeFunc()
    {
        gm.transform.SetParent(nullPar.transform);
    }
}
