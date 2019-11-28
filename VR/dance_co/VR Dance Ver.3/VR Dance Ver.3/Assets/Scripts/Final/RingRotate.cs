using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class RingRotate : MonoBehaviour
{
    void Update()
    {
        gameObject.transform.Rotate(Vector3.up * 90f * Time.deltaTime);
    }
}
