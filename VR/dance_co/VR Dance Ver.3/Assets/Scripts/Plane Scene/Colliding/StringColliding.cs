using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class StringColliding : MonoBehaviour
{
    MakeBackground mBack;

    private void Start()
    {
        mBack = GameObject.Find("GameObject").GetComponent<MakeBackground>();
    }

    private void OnTriggerEnter(Collider other)
    {
        if(other.tag == "Tracker")
        {
            if (!mBack.start)
            {
                mBack.start = true;
            }

            if(!mBack.col && mBack.firstPlaneSet)
            {
                mBack.col = true;
            }
        }
    }
}
