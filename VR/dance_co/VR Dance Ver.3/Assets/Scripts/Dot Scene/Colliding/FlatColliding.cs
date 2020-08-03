using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FlatColliding : MonoBehaviour
{
    public GameObject nullParent;
    Flat flat;

    void Start()
    {
        flat = GameObject.Find("FlatManager").GetComponent<Flat>();
    }

    private void OnTriggerEnter(Collider other)
    {
        if(other.tag == "Tracker")
        {
            if(flat.moveStart)
            {
                for (int i = 0; i < other.gameObject.transform.childCount; i++)
                {
                    other.gameObject.transform.GetChild(i).SetParent(nullParent.transform);
                }

                gameObject.transform.SetParent(other.transform);
            }
        }   
    }
}