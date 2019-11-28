using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class spring_stick : MonoBehaviour
{
    public GameObject nullPar, spring_Sticks;
    bool coll;

    private void Start()
    {
        coll = false;
    }

    void Update()
    {
        if(coll)
        {
            if(spring_Sticks.transform.localScale.x >= 1f)
            {
                spring_Sticks.transform.localScale -= new Vector3(0.03f, 0, 0);
            }

            if(spring_Sticks.transform.localScale.y >= 1f)
            {
                spring_Sticks.transform.localScale -= new Vector3(0, 0.09f, 0);
            }

            if(spring_Sticks.transform.localScale.z >= 1f)
            {
                spring_Sticks.transform.localScale -= new Vector3(0, 0, 0.03f);
            }

            spring_Sticks.transform.localPosition = Vector3.MoveTowards(spring_Sticks.transform.localPosition,
                new Vector3(-3, -2.83f, -2.19f), 1.0f * Time.deltaTime);
        }
    }

    private void OnTriggerEnter(Collider other)
    {
        if(other.tag == "Tracker")
        {
            coll = true;
            for(int i=0;i<other.transform.childCount;i++)
            {
                other.transform.GetChild(i).SetParent(nullPar.transform);
            }

            spring_Sticks.transform.SetParent(other.transform);
        }
    }
}
