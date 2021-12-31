using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class temp1 : MonoBehaviour
{
    public CameraMove move;

    public void to3D()
    {
        move.camera3D = true;
    }

    public void to2D()
    {
        move.camera3D = false;
    }
}
