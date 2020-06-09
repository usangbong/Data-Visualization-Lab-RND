using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using MLAgents;

public class RadiusCollocateTest : Agent
{
    public Transform pivot, target;

    Vector3 originPos, originRot;

    IntegratedCorWrong cw;
    CollocateManager cm;

    float averageRadius = 0, radius;
    int countRadius = 0, select;

    void Awake()
    {
        cw = GameObject.Find("CorWrong").GetComponent<IntegratedCorWrong>();
        cm = GameObject.Find("setObjectManager").GetComponent<CollocateManager>();

        StartCoroutine(timeChecker());
    }

    public void setOrigin(Transform target)
    {
        originPos = target.position;
        originRot = target.rotation.eulerAngles;
    }

    public override void CollectObservations()
    {
        AddVectorObs(originPos);
        AddVectorObs(target.position);
        AddVectorObs(radius);
        AddVectorObs(averageRadius);
        AddVectorObs(select);
    }

    public override void AgentAction(float[] vectorAction)
    {
        select = Mathf.FloorToInt(vectorAction[0]);

        radius = Vector3.Distance(originPos, target.position);
        averageRadius = averageRadius + (radius - averageRadius) / ++countRadius;
        
        if(select == 0)
        {
            if(radius >= averageRadius)
            {
                cw.rCorrect++;
                cm.setWide(true);
                AddReward(1f);
            }

            else
            {
                cw.rWrong++;
                cm.setWide(false);
                AddReward(-1f);
            }
        }

        else if(select == 1)
        {
            if(radius >= averageRadius)
            {
                cw.rWrong++;
                cm.setWide(true);
                AddReward(-1f);
            }

            else
            {
                cw.rCorrect++;
                cm.setWide(false);
                AddReward(1f);
            }
        }
    }

    IEnumerator timeChecker()
    {
        while (true)
        {
            yield return new WaitForSeconds(100f);

            cw.change = true;
            Done();
        }
    }
}
