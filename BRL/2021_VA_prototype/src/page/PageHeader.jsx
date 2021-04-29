import './PageHeader.scoped.scss';

function PageHeader(props) {
  return (
    <div className="PageHeader">
      {props.msg}
    </div>
  );
}

export default PageHeader;
