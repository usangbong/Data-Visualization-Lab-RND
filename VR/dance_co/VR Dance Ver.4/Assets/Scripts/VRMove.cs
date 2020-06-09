using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class VRMove : MonoBehaviour
{
    public float moveSpeed;

    void Update()
    {
        if(Input.GetAxis("Horizontal") > 0)
        {
            transform.Translate(Vector3.right * moveSpeed * Time.deltaTime);
        }

        else if (Input.GetAxis("Horizontal") < 0)
        {
            transform.Translate(Vector3.left * moveSpeed * Time.deltaTime);
        }

        if (Input.GetAxis("Vertical") > 0)
        {
            transform.Translate(Vector3.forward * moveSpeed * Time.deltaTime);
        }

        else if (Input.GetAxis("Vertical") < 0)
        {
            transform.Translate(Vector3.back * moveSpeed * Time.deltaTime);
        }


        if (Input.GetAxis("Jump") > 0)
        {
            transform.Translate(Vector3.up * moveSpeed * Time.deltaTime);
        }

        else if (Input.GetAxis("Jump") < 0)
        {
            transform.Translate(Vector3.down * moveSpeed * Time.deltaTime);
        }
    }
}
