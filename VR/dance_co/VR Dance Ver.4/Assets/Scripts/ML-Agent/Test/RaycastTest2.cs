using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using MLAgents;

public class RaycastTest2 : Agent
{
    public float moveForce;
    public int idx;
    Vector3 originPos, originRot;
    Rigidbody rigidBody;

    GameObject head;

    HeadRaycast hRay;
    CorWrong cw;

    bool isHit = false;

    void Awake()
    {
        rigidBody = GetComponent<Rigidbody>();
        originPos = transform.position;
        originRot = transform.rotation.eulerAngles;

        head = GameObject.Find("Head");
        hRay = GameObject.Find("Head").GetComponent<HeadRaycast>();
        cw = GameObject.Find("CorWrong").GetComponent<CorWrong>();
    }

    void ResetTarget()
    {
        rigidBody.velocity = Vector3.zero;
        transform.position = originPos;
        transform.rotation = Quaternion.Euler(originRot);
    }

    public override void AgentReset()
    {
        ResetTarget();
    }

    public override void CollectObservations()
    {
        AddVectorObs(hRay.avgVelocity);
        AddVectorObs(rigidBody.velocity);
        AddVectorObs(transform.position);
        AddVectorObs(head.transform.rotation.eulerAngles);
        AddVectorObs(isHit);
    }

    void Update()
    {
        hRay.velList[idx] = rigidBody.velocity.magnitude;
    }

    public override void AgentAction(float[] vectorAction)
    {
        rigidBody.AddForce(vectorAction[0] * moveForce, vectorAction[1] * moveForce, vectorAction[2] * moveForce);

        if(isHit)
        {
            if(rigidBody.velocity.magnitude >= hRay.avgVelocity)
            {
                AddReward(5f/150f);
                cw.correct += 1;
            }

            else
            {
                AddReward(-(1f/150f));
                cw.wrong += 1;
            }
        }

        else
        {
            if (rigidBody.velocity.magnitude >= hRay.avgVelocity)
            {
                AddReward(-(1f/150f));
                cw.wrong += 1;
            }

            else
            {
                AddReward(5f/150f);
                cw.correct += 1;
            }
        }

        //1초당 150번 실행됨: 그래소요 오쪼로고요
        //음 , , , , 더 쉬 운 방 법 을 찾 아 야 한 다
        //AddReward를 한번?음 음 으 ㅁ 으 ㅁㅇ ㅡㅁ낭
    }

    public void setHit(bool ishit)
    {
        isHit = ishit;
    }

    private void OnTriggerEnter(Collider other)
    {
        if(other.tag == "dead")
        {
            AddReward(-1f);
            ResetTarget();
        }
    }
}
