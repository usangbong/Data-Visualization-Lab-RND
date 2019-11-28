using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TranslateTorus : MonoBehaviour
{
    bool rot;
    Final final;

    private void Start()
    {
        rot = false;
        final = GameObject.Find("GameManager").GetComponent<Final>();
    }

    private void Update()
    {
        if(rot && !final.timeFin)
        {
            gameObject.transform.Rotate(new Vector3(1,1,1) * 45f * Time.deltaTime);
        }
    }

    private void OnTriggerEnter(Collider other)
    {
        if(other.tag == "Tracker")
        {
            rot = true;
        }
    }
}
