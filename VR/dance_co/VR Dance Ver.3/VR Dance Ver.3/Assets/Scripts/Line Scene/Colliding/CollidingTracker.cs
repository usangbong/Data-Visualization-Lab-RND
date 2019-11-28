using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CollidingTracker : MonoBehaviour
{
    public GameObject nullParent;
    Spring spring;

    void Start()
    {
        spring = GameObject.Find("SpringManager").GetComponent<Spring>();
    }

    private void OnTriggerEnter(Collider other)
    {
        if(other.tag == "Tracker")
        {
            if(!spring.isSize)
            {
                for(int i=0;i<other.gameObject.transform.childCount;i++)
                {
                    other.gameObject.transform.GetChild(i).SetParent(nullParent.transform);
                }

                gameObject.transform.SetParent(other.transform);
            }
        }
    }
}
