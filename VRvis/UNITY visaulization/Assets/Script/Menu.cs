using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Menu : MonoBehaviour
{

    private float count = 0.0f;
    public float moveSpeed;
    public GameObject cam;
    
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
            if(gameObject.name == "up") { cam.transform.Translate(Vector3.up * moveSpeed * Time.deltaTime); }
            else if (gameObject.name == "front") { cam.transform.Translate(Vector3.forward * moveSpeed * Time.deltaTime); }
            else if (gameObject.name == "down") { cam.transform.Translate(Vector3.down * moveSpeed * Time.deltaTime); }
            else if (gameObject.name == "back") { cam.transform.Translate(Vector3.back * moveSpeed * Time.deltaTime); }
            else if (gameObject.name == "left") { cam.transform.Translate(Vector3.left * moveSpeed * Time.deltaTime); }
            else if (gameObject.name == "right") { cam.transform.Translate(Vector3.right * moveSpeed * Time.deltaTime); }
            else if (gameObject.name == "left_turn") { cam.transform.Rotate(Vector3.down * moveSpeed * Time.deltaTime); }
            else if (gameObject.name == "right_turn") { cam.transform.Rotate(Vector3.up * moveSpeed * Time.deltaTime); }
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
