using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.MLAgents;
using Unity.MLAgents.Sensors;
using System.Linq;
using UnityEngine.Serialization;
using System;
using System.IO;
using System.Reflection;

public class CellAgent : Agent
{
    public OfficeArea area;
    public Transform obj;
    public SnapAgent snap;

    bool isSnap;

    public override void Initialize()
    {
        isSnap = false;
        area.CellReset();
    }

    public override void OnEpisodeBegin()
    {

    }

    public override void CollectObservations(VectorSensor sensor)
    {
        //Cell Object Count Observation
        List<List<Cell>> cells = area.getAllCells();

        for (int i = 0; i < area.z_Count; i++)
        {
            for (int j = 0; j < area.x_Count; j++)
            {
                sensor.AddObservation(cells[i][j].getObjectCount());
            }
        }

    }

    public override void OnActionReceived(float[] vectorAction)
    {
        float action = vectorAction[0];

        //Cell을 받아와서 cell에 오브젝트 추가 후 해당 오브젝트를 Cell로 이동
        Cell cell = setObjectCell(action);
        obj.position = cell.getCenterPos();

        /*//벗어난게 있으면 벗어난것 * 0.25점 감점
        for (int state = (int)OfficeArea.OverState.OVER_RIGHT; state <= (int)OfficeArea.OverState.OVER_DOWN; state++)
        {
            if (cell.isOverObject(obj.gameObject, state)) AddReward(-0.25f);
        }
        */

        //Cell을 벗어난 부분에 Object 추가
        area.SearchOverTheCellObjectAndAddObjectToCell(cell, obj.gameObject);
    }

    Cell setObjectCell(float action)
    {
        Cell cell = area.FindCellByIndex(System.Convert.ToInt32(action));
        cell.AddObject(obj.gameObject);

        return cell;
    }

    public void setSnap(float _action)
    {
        if (_action == 1) isSnap = true;
        else isSnap = false;
    }
}
