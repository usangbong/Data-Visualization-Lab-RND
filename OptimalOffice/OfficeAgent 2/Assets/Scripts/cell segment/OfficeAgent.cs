using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.MLAgents;
using Unity.MLAgents.Sensors;
using System.Linq;
using UnityEngine.Serialization;
using System;
using System.IO;

public class OfficeAgent : Agent
{
    public OfficeArea area;
    public PlayerMove player;
    public Transform obj;

    Cell cell;

    float action = 0f;
    float time;

    public override void Initialize()
    {
        time = 0f;
        area.CellReset();
    }

    public override void OnEpisodeBegin()
    {
        time = 0f;
        area.CellReset();
    }

    public override void CollectObservations(VectorSensor sensor)
    {
        //sensor.AddObservation(gameObject.GetComponent<ObjectConfig>().isHorizontalSnap);
        //sensor.AddObservation(gameObject.GetComponent<ObjectConfig>().isVerticalSnap);

        //Cell Index Observation
        sensor.AddObservation(action);

        //Cell Object Count Observation
        List<List<Cell>> cells = area.getAllCells();

        for (int i = 0; i < 5; i++)
        {
            for (int j = 0; j < 8; j++)
            {
                sensor.AddObservation(cells[i][j].getObjectCount());
            }
        }

        /*
        for(int i=0;i<5;i++)
        {
            for(int j=0;j<8;j++)
            {
                int cnt = cells[i][j].getObjectCount();
                List<GameObject> objList = cells[i][j].getObjectList();

                for(int k=0;k<cnt;k++)
                {
                    if (objList[k] == gameObject) sensor.AddObservation(cells[i][j].getIdx());
                }
            }
        }
        */

        cell = area.FindCellByIndex(System.Convert.ToInt32(action));
        //Object Over the Cell Observation
        for (int state = (int)OfficeArea.OverState.OVER_RIGHT; state <= (int)OfficeArea.OverState.OVER_DOWN; state++)
        {
            sensor.AddObservation(cell.isOverObject(obj.gameObject, state));
        }
    }

    public override void OnActionReceived(float[] vectorAction)
    {
        action = vectorAction[0];

        //Cell을 받아와서 cell에 오브젝트 추가 후 해당 오브젝트를 Cell로 이동
        cell = area.FindCellByIndex(System.Convert.ToInt32(action));
        cell.AddObject(obj.gameObject);
        obj.transform.position = cell.getCenterPos();

        //벗어난게 있으면 벗어난것 * 0.25점 감점
        for (int state = (int)OfficeArea.OverState.OVER_RIGHT; state <= (int)OfficeArea.OverState.OVER_DOWN; state++)
        {
            if (cell.isOverObject(obj.gameObject, state)) AddReward(-0.25f);
        }

        //Cell을 벗어난 부분에 Object 추가
        area.SearchOverTheCellObjectAndAddObjectToCell(cell, obj.gameObject);

        /*
        //수평 snap 비교
        if(gameObject.GetComponent<ObjectConfig>().isHorizontalSnap)
        {
            if (area.isHorizontalSnap(cell.getIdx())) AddReward(1f);
            else AddReward(-1f);
        }

        //수직 snap 비교
        if(gameObject.GetComponent<ObjectConfig>().isVerticalSnap)
        {
            if (area.isVerticalSnap(cell.getIdx())) AddReward(1f);
            else AddReward(-1f);
        }
        */
    }

    //0.01초마다 한번씩 Duplicate된 Cell에 존재하는 Object의 Agent에 감점주고 Decision Request
    private void FixedUpdate()
    {
        time += Time.fixedDeltaTime;
        if (time >= 0.01f)
        {
            area.FindDuplicateCellAndDeductionToObject();
            RequestDecision();
        }
    }
}
