using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.MLAgents;
using Unity.MLAgents.Sensors;
using System.Linq;
using UnityEngine.Serialization;
using System;
using System.IO;

public class OfficeAgent :Agent
{
    private void Start()
    {
        if (random) action = UnityEngine.Random.Range(0, 40);

        Cell cell = area.FindCellByIndex(action);
        cell.AddObject(gameObject);
        cell.cellObj.GetComponent<MeshRenderer>().material.color = Color.yellow;

        gameObject.transform.position = cell.getCenterPos();

        area.SearchOverTheCellObjectAndAddObjectToCell(cell, transform.GetChild(0).gameObject);
    }

    private void Update()
    {
        time += Time.deltaTime;

        if(time > 3f)
        {
            area.FindDuplicateCellAndDeductionToObject();
        }
    }

    /*public OfficeArea area;
    public PlayerMove player;
    public Transform obj;

    public Camera renderCamera;
   
    public override void Initialize()
    {

    }

    public override void OnEpisodeBegin()
    {

    }

    public override void OnActionReceived(float[] vectorAction)
    {
        float action = vectorAction[0];

        Cell cell = area.FindCellByIndex(System.Convert.ToInt32(action));
        cell.AddObject(gameObject);
        transform.position = cell.getCenterPos();
        if (cell.isOverObject(gameObject) == (int)OfficeArea.OverState.NOT_OVER) AddReward(-1f);

        area.SearchOverTheCellObjectAndAddObjectToCell(cell, gameObject);

        if(gameObject.GetComponent<ObjectConfig>().isHorizontalSnap)
        {
            if (area.isHorizontalSnap(cell.getIdx())) AddReward(1f);
            else AddReward(-1f);
        }

        if(gameObject.GetComponent<ObjectConfig>().isVerticalSnap)
        {
            if (area.isVerticalSnap(cell.getIdx())) AddReward(1f);
            else AddReward(-1f);
        }
    }

    private void FixedUpdate()
    {
        if (renderCamera != null)
        {
            renderCamera.Render();
        }

        if(player.isMoveFinish)
        {
            player.finIdx++;
            if (player.finIdx > 7)
            {
                player.isMoveFinish = false;
                player.finIdx = 0;
            }
            RequestDecision();
        }
    }*/
}
