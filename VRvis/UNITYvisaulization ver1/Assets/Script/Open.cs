using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Open : MonoBehaviour
{
    public float moveSpeed;
    private float count = 0.0f;

    public GameObject cam;
    public GameObject close;
    public GameObject menu;
    public GameObject On;

    public Material red;
    public Material black;


    void OnTriggerEnter(Collider col)
    {
        if (col.tag == "Laser")
        {

            GetComponent<MeshRenderer>().material = red;
        }
    }

    void OnTriggerStay(Collider col)
    {
        if (count >= 1f)
        {
            close.SetActive(true);
            menu.SetActive(true);
            GetComponent<MeshRenderer>().material = black;
            count = 0.0f;
            On.SetActive(false);
        }
        if (col.tag == "Laser")
        {
            count += (1 / 60f);
        }
    }

    void OnTriggerExit(Collider col)
    {
        if (col.tag == "Laser")
        {
            count = 0.0f;
            GetComponent<MeshRenderer>().material = black;
        }
    }

}
