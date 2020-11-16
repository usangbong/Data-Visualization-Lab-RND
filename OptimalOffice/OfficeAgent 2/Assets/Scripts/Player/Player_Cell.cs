using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Player_Cell : MonoBehaviour
{
    int cell_idx;
    Vector3 centerPos;
    
    public Player_Cell(int idx, float center_x, float center_z)
    {
        cell_idx = idx;

        centerPos = new Vector3(center_x, 0, center_z);
    }

    public int getCellIndex() { return cell_idx; }
    public Vector3 getCenterPos() { return centerPos; }
}
