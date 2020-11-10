using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.MLAgents;
using Unity.MLAgents.Sensors;

public class SnapAgent : Agent
{
    public OfficeArea area;
    public Transform obj;

    public CellAgent cell;

    float action;

    bool next;

    public override void Initialize()
    {
        next = false;
        RequestDecision();
    }

    public override void OnEpisodeBegin()
    {
        
    }

    public override void CollectObservations(VectorSensor sensor)
    {
        sensor.AddObservation(obj.GetComponent<ObjectConfig>().isHorizontalSnap);
        sensor.AddObservation(obj.GetComponent<ObjectConfig>().isVerticalSnap);
    }

    public override void OnActionReceived(float[] vectorAction)
    {        
        action = vectorAction[0];

        if (obj.GetComponent<ObjectConfig>().isHorizontalSnap)
        {

        }

        if(obj.GetComponent<ObjectConfig>().isVerticalSnap)
        {

        }

        cell.RequestDecision();
    }
}
