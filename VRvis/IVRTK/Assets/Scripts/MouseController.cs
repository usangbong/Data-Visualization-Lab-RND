using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MouseController : MonoBehaviour
{
    public GameObject obj;
    bool isDown;

    public float moveSpeed = 1f;
    public float rotateSpeed = 1f;
    void Start()
    {
        isDown = false;
    }

    // Update is called once per frame
    void Update()
    {
        Vector2 wheelInput = Input.mouseScrollDelta;
        if (Input.GetMouseButton(0))
        {
            obj.transform.rotation = Quaternion.Euler(new Vector3(obj.transform.rotation.eulerAngles.x, obj.transform.rotation.eulerAngles.y + rotateSpeed, obj.transform.rotation.eulerAngles.z));
        }
        if (Input.GetMouseButton(1))
        {
            obj.transform.rotation = Quaternion.Euler(new Vector3(obj.transform.rotation.eulerAngles.x, obj.transform.rotation.eulerAngles.y - rotateSpeed, obj.transform.rotation.eulerAngles.z));
        }
        if (Input.GetMouseButtonDown(2)) {
            isDown = true;
        }
        if (Input.GetMouseButtonUp(2))
        {
            isDown = false;
        }
        if (!isDown)
        {
            if (wheelInput.y > 0)
            {
                obj.transform.position = new Vector3(obj.transform.position.x, obj.transform.position.y , obj.transform.position.z + moveSpeed);
            }
            else if (wheelInput.y < 0)
            {
                obj.transform.position = new Vector3(obj.transform.position.x, obj.transform.position.y , obj.transform.position.z - moveSpeed);
            }
        }
        else
        {
            float rotateSpeed2 = rotateSpeed * 5f;
            if (wheelInput.y > 0)
            {
                obj.transform.rotation = Quaternion.Euler(new Vector3(obj.transform.rotation.eulerAngles.x + rotateSpeed2, obj.transform.rotation.eulerAngles.y, obj.transform.rotation.eulerAngles.z));
            }
            else if (wheelInput.y < 0)
            {
                obj.transform.rotation = Quaternion.Euler(new Vector3(obj.transform.rotation.eulerAngles.x - rotateSpeed2, obj.transform.rotation.eulerAngles.y, obj.transform.rotation.eulerAngles.z));              
            }
        }
        if (Input.GetMouseButton(3))
        {
            obj.transform.position = new Vector3(obj.transform.position.x, obj.transform.position.y - moveSpeed, obj.transform.position.z);
        }
        if (Input.GetMouseButton(4))
        {
            obj.transform.position = new Vector3(obj.transform.position.x, obj.transform.position.y + moveSpeed, obj.transform.position.z);
        }
    }
}
