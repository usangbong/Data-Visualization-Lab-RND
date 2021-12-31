using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraMove : MonoBehaviour
{
    public Camera camera;
    public bool camera3D = false;

    private void Update()
    {
        if (camera3D)
        {
            Camera.main.orthographic = false;
            Camera.main.transform.position = Vector3.MoveTowards(Camera.main.transform.position,
                new Vector3(0, 13.86f, -10.64f), Time.deltaTime * 3.0f);
            Camera.main.transform.rotation = Quaternion.Lerp(Camera.main.transform.rotation,
                Quaternion.Euler(new Vector3(60, 0, 0)), Time.deltaTime * 2.0f);
        }

        else
        {
            Camera.main.transform.position = Vector3.MoveTowards(Camera.main.transform.position,
                new Vector3(0, 20, 0), Time.deltaTime * 3.0f);
            Camera.main.transform.rotation = Quaternion.Lerp(Camera.main.transform.rotation,
                Quaternion.Euler(new Vector3(90, 0, 0)), Time.deltaTime * 2.0f);

            if(Camera.main.transform.position == new Vector3(0,20,0) && 
                Camera.main.transform.rotation == Quaternion.Euler(new Vector3(90, 0, 0)))
            {
                Camera.main.orthographic = true;
            }
        }
    }
}
