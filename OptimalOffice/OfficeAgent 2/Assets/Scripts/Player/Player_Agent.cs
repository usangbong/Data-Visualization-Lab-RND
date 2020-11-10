using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.MLAgents;
using Unity.MLAgents.Sensors;

public class Player_Agent : Agent
{
    Player_Area area;
    Player_Cell cell, nextCell;

    const int STAY = 0;
    const int RIGHT = 1;
    const int LEFT = 2;
    const int UP = 3;
    const int DOWN = 4;

    public override void Initialize()
    {
        area = GameObject.Find("AreaManager").GetComponent<Player_Area>();

        cell = area.findCell(gameObject);
    }

    public override void OnEpisodeBegin()
    {
        
    }

    public override void CollectDiscreteActionMasks(DiscreteActionMasker actionMasker)
    {
        
    }

    public override void CollectObservations(VectorSensor sensor)
    {
        
    }

    public override void OnActionReceived(float[] vectorAction)
    {
        float action = vectorAction[0];

        switch(action)
        {
            case STAY:
                nextCell = cell;
                break;
            case RIGHT:
                nextCell = area.getNextCell(cell, Info.RIGHT);
                break;
            case LEFT:
                nextCell = area.getNextCell(cell, Info.LEFT);
                break;
            case UP:
                nextCell = area.getNextCell(cell, Info.UP);
                break;
            case DOWN:
                nextCell = area.getNextCell(cell, Info.DOWN);
                break;
        }

        gameObject.transform.position = nextCell.getCenterPos();
    }
}
