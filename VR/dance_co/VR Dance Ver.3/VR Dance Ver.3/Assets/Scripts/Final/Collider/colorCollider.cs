using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class colorCollider : MonoBehaviour
{
    ColorFiercing Cf;

    private void Start()
    {
        Cf = GameObject.Find("ColorManager").GetComponent<ColorFiercing>();
    }

    private void OnTriggerEnter(Collider other)
    {
        if(other.tag == "Tracker")
        {
            if (!Cf.parent)
            {
                other.transform.DetachChildren();
                Cf.c1.transform.SetParent(other.transform);
                Cf.c2.transform.SetParent(other.transform);
                Cf.c3.transform.SetParent(other.transform);
                Cf.tmp = other.gameObject;
                Cf.parent = true;
            }
        }
    }
}
