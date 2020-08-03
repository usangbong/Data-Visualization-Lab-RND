using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EyeCollider : MonoBehaviour
{
    bool isColliding, down;

    void Start()
    {
        isColliding = down = false;
    }

    void Update()
    {
        if(isColliding && !down)
        {
            gameObject.transform.GetChild(1).transform.localRotation = Quaternion.Slerp(
                gameObject.transform.GetChild(1).transform.localRotation,
                Quaternion.Euler(0, 0, 0), 3.0f * Time.deltaTime);

            gameObject.transform.GetChild(2).transform.localRotation = Quaternion.Slerp(
                gameObject.transform.GetChild(2).transform.localRotation,
                Quaternion.Euler(-180, 0, 0), 3.0f * Time.deltaTime);

            if(gameObject.transform.GetChild(1).transform.localRotation == Quaternion.Euler(0,0,0) &&
                gameObject.transform.GetChild(2).transform.localRotation == Quaternion.Euler(-180, 0, 0))
            {
                gameObject.transform.GetChild(1).transform.localRotation = Quaternion.Euler(0, 0, 0);
                gameObject.transform.GetChild(2).transform.localRotation = Quaternion.Euler(-180, 0, 0);
                down = true;
            }
        }

        if(isColliding && down)
        {
            gameObject.transform.GetChild(1).transform.localRotation = Quaternion.Slerp(
                gameObject.transform.GetChild(1).transform.localRotation,
                Quaternion.Euler(-50, 0, 0), 3.0f * Time.deltaTime);
            gameObject.transform.GetChild(2).transform.localRotation = Quaternion.Slerp(
                gameObject.transform.GetChild(2).transform.localRotation,
                Quaternion.Euler(-120, 0, 0), 3.0f * Time.deltaTime);

            if (gameObject.transform.GetChild(1).transform.localRotation == Quaternion.Euler(-50, 0, 0) &&
                gameObject.transform.GetChild(2).transform.localRotation == Quaternion.Euler(-120, 0, 0))
            {
                gameObject.transform.GetChild(1).transform.localRotation = Quaternion.Euler(-50, 0, 0);
                gameObject.transform.GetChild(2).transform.localRotation = Quaternion.Euler(-120, 0, 0);

                down = false;
                isColliding = false;
            }
        }
    }

    private void OnTriggerEnter(Collider other)
    {
        if(other.tag == "Tracker")
        {
            isColliding = true;
        }
    }
}
