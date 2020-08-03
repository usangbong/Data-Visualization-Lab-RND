using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ObjectMove : MonoBehaviour
{
    public float speed = 1.0f;
    public bool fin = true;

    void Update()
    {
        if(fin) transform.Translate(Vector3.forward * speed * Time.deltaTime);
    }
}
