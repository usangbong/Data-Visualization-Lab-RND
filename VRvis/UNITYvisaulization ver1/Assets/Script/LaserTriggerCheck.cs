using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Collections;

public class LaserTriggerCheck : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    private void OnTriggerEnter(Collider other)
    {
        if (other.gameObject.CompareTag("Object"))
        {
            Debug.Log("TriggerCheck!");
            Debug.Log("Trigger Position : " + other.transform.position);
        }
    }

    private void OnTriggerStay(Collider other)
    {
        if (other.gameObject.CompareTag("Object")) {
            Debug.Log("TriggerStay!" + other.name);
        }
    }
    private void OnTriggerExit(Collider other)
    {
        if (other.gameObject.CompareTag("Object"))
        {
            Debug.Log("Trigger Out Check");
        }   
    }
    private void OnCollisionEnter(Collision other)
    {
        Debug.Log("On Collision Enter");
        Debug.Log("Test : " + other.collider.tag);
       // Vector3 pos_t = other.contacts[0].point;
        //Debug.Log("Collistion Vector Check ! " + pos_t);

        if (other.collider.CompareTag("Object"))
        {
            Vector3 pos = other.contacts[0].point;
            Debug.Log("Collistion Vector Check ! : " + other.gameObject.name + pos);
        }
    }

    private void OnCollisionStay(Collision other)
    {
        if (other.collider.CompareTag("Object"))
        {
            Vector3 pos = other.contacts[0].point;
            Debug.Log("Collistion Vector Stay ! : " + other.collider.name + pos);
        }
    }
}
