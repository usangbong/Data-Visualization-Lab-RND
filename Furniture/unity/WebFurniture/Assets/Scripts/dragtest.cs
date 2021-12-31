using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class dragtest : MonoBehaviour
{
    public Transform target = null;

    private void Update()
    {
        if(Input.GetMouseButton(0))
        {
            var Point = Camera.main.ScreenToWorldPoint(new Vector3(Input.mousePosition.x, Input.mousePosition.y,
                -Camera.main.transform.position.z));
            Point.y = 0.5f;

            target.position = Point;
        }
    }
}
