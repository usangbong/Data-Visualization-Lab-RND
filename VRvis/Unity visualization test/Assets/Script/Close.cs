using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Close : MonoBehaviour
{
    float count = 0.0f;
    public float moveSpeed;
    public GameObject cam;
    public GameObject open;
    public GameObject menu;
    public GameObject exit;

    public Material red;
    public Material black;


    void OnTriggerEnter(Collider col) { 
        if(col.tag == "Laser")
        {

            GetComponent<MeshRenderer>().material = red; 
        }
    }
    
    void OnTriggerStay(Collider col)
    {
        if (count >= 1f)
        {
            open.SetActive(true);
            menu.SetActive(false);
            GetComponent<MeshRenderer>().material = black;
            count = 0.0f;
            exit.SetActive(false);
        }
        if (col.tag == "Laser")
        {
            count += (1/60f);
        }
    }

    void OnTriggerExit(Collider col)
    {
        if(col.tag == "Laser")
        {
            count = 0.0f;
            GetComponent<MeshRenderer>().material = black;
        }
    }
}
